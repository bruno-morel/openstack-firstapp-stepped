package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/secgroups"
	"github.com/rackspace/gophercloud/pagination"
	"github.com/smallfish/simpleyaml"
)

func main() {
	type CloudConfig struct {
		UserName       string
		Password       string
		ProjetOrTenant string
		Region         string
		AuthURL        string
	}

	var config CloudConfig

	yamldata, err := ioutil.ReadFile("clouds.yaml")
	if err != nil {
		panic(err)
	}
	yaml, err := simpleyaml.NewYaml(yamldata)
	if err != nil {
		panic(err)
	}
	config.AuthURL, err = yaml.Get("clouds").Get("internap").Get("authUrl").String()
	if err != nil {
		panic(err)
	}
	config.UserName, err = yaml.Get("clouds").Get("internap").Get("auth").Get("username").String()
	if err != nil {
		panic(err)
	}
	config.Password, err = yaml.Get("clouds").Get("internap").Get("auth").Get("password").String()
	if err != nil {
		panic(err)
	}
	config.ProjetOrTenant, err = yaml.Get("clouds").Get("internap").Get("auth").Get("project_name").String()
	if err != nil {
		panic(err)
	}
	config.Region, err = yaml.Get("clouds").Get("internap").Get("region_name").String()
	if err != nil {
		panic(err)
	}

	provider, err := openstack.AuthenticatedClient(gophercloud.AuthOptions{
		IdentityEndpoint: config.AuthURL,
		Username:         config.UserName,
		Password:         config.Password,
		TenantName:       config.ProjetOrTenant,
	})
	if err != nil {
		fmt.Println(err)
		return
	}
	const secgroupName string = "all-in-one"
	const secgroupDescription string = "network access for all-in-one application."
	var ptrSecgroupFound *secgroups.SecurityGroup

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Printf("Looking for security group named '%s'...\n", secgroupName)
	secgroups.List(nova).EachPage(func(page pagination.Page) (bool, error) {
		secgroupsList, err := secgroups.ExtractSecurityGroups(page)

		if err != nil {
			return false, err
		}

		for _, currentSGroup := range secgroupsList {
			if strings.Contains(currentSGroup.Name, secgroupName) {
				ptrSecgroupFound = &currentSGroup
			}
		}
		return true, nil
	})

	if ptrSecgroupFound != nil {
		fmt.Println("\tfound it, skipping creation")
		fmt.Println("Done! Congrats")
		return
	}

	fmt.Println("\tnot found, creating the security group")
	opts := secgroups.CreateOpts{
		Name:        secgroupName,
		Description: secgroupDescription,
	}
	group, err := secgroups.Create(nova, opts).Extract()
	if err != nil {
		panic(err)
	}
	_, err = secgroups.CreateRule(nova, secgroups.CreateRuleOpts{ParentGroupID: group.ID, FromPort: 80, ToPort: 80, IPProtocol: "TCP", CIDR: "0.0.0.0/0"}).Extract()
	_, err = secgroups.CreateRule(nova, secgroups.CreateRuleOpts{ParentGroupID: group.ID, FromPort: 22, ToPort: 22, IPProtocol: "TCP", CIDR: "0.0.0.0/0"}).Extract()
	if err != nil {
		panic(err)
	}

	fmt.Println("Done! Congrats")
}
