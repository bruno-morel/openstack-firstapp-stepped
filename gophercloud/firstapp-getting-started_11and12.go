package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/keypairs"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/networks"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/secgroups"
	"github.com/rackspace/gophercloud/openstack/compute/v2/images"
	"github.com/rackspace/gophercloud/openstack/compute/v2/servers"
	"github.com/rackspace/gophercloud/openstack/db/v1/flavors"
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
	config.AuthURL, err = yaml.Get("clouds").Get("internapNYJ").Get("authUrl").String()
	if err != nil {
		panic(err)
	}
	config.UserName, err = yaml.Get("clouds").Get("internapNYJ").Get("auth").Get("username").String()
	if err != nil {
		panic(err)
	}
	config.Password, err = yaml.Get("clouds").Get("internapNYJ").Get("auth").Get("password").String()
	if err != nil {
		panic(err)
	}
	config.ProjetOrTenant, err = yaml.Get("clouds").Get("internapNYJ").Get("auth").Get("project_name").String()
	if err != nil {
		panic(err)
	}
	config.Region, err = yaml.Get("clouds").Get("internapNYJ").Get("region_name").String()
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

	const instanceName string = "testing for gophercloud"
	const keypairName string = "demokey"
	const secgroupName string = "all-in-one"
	const secgroupDescription string = "network access for all-in-one application."

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	var netWAN []servers.Network
	fmt.Println("Listing networks...")
	err = networks.List(nova).EachPage(func(page pagination.Page) (bool, error) {
		networkPage, err := networks.ExtractNetworks(page)
		if err != nil {
			return false, err
		}

		for _, currentNetwork := range networkPage {
			if strings.Contains(currentNetwork.Label, "WAN") {
				fmt.Printf("\t found WAN network with name : %s\n", currentNetwork.Label)
				netWAN = []servers.Network{servers.Network{UUID: currentNetwork.ID}}
			}
		}

		return true, nil
	})
	if err != nil {
		fmt.Println(err)
		return
	}

	flavor, err := flavors.Get(nova, "A1.1").Extract()

	image, err := images.Get(nova, "3c76334f-9644-4666-ac3c-fa090f175655").Extract()

	var ptrSecgroupFound *secgroups.SecurityGroup
	fmt.Printf("Checking for security group named '%s'...\n", secgroupName)
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
	} else {
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
	}

	// step-11
	userdata := "#!/bin/bash\ncurl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- -i faafo -i messaging -r api -r worker -r demo"

	// step-12
	fmt.Println("Checking if instance already exists...")
	var ptrServerFound *servers.Server
	servers.List(nova, servers.ListOpts{Name: instanceName}).EachPage(func(page pagination.Page) (bool, error) {
		serverList, err := servers.ExtractServers(page)
		if err != nil {
			return false, err
		}

		for _, currentServer := range serverList {
			if strings.Contains(currentServer.Name, instanceName) {
				ptrServerFound = &currentServer
			}
		}
		return true, nil
	})

	if ptrServerFound != nil {
		fmt.Println("\tserver exists, skipping creation")
		fmt.Println("Done! Congrats")
		return
	}
	fmt.Println("Creating instance...")

	server, err := servers.Create(nova, keypairs.CreateOptsExt{servers.CreateOpts{Name: instanceName, FlavorRef: flavor.ID, ImageRef: image.ID, UserData: []byte(userdata), Networks: netWAN, SecurityGroups: []string{secgroupName}}, keypairName}).Extract()
	if err != nil {
		fmt.Printf("\tunable to create server: %s", err)
	}
	fmt.Printf("\tcreated server with ID: %s", server.ID)

	fmt.Println("Listing all active instance...")
	servers.List(nova, servers.ListOpts{}).EachPage(func(page pagination.Page) (bool, error) {
		serverList, err := servers.ExtractServers(page)
		if err != nil {
			return false, err
		}

		for _, s := range serverList {
			fmt.Println(s.ID, s.Name, s.Status)
		}
		return true, nil
	})
	fmt.Println("Done! Congrats")
}
