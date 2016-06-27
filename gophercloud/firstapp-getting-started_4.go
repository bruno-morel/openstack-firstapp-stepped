package main

import (
	"fmt"
	"io/ioutil"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/flavors"
	"github.com/rackspace/gophercloud/openstack/compute/v2/images"
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

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	image, err := images.Get(nova, "3c76334f-9644-4666-ac3c-fa090f175655").Extract()
	if err != nil {
		fmt.Printf("Unable to find image: %s\n", err)
		return
	}
	fmt.Printf("Selected image: %s\n", image)

	flavor, err := flavors.Get(nova, "A1.1").Extract()
	if err != nil {
		fmt.Printf("Unable to find flavor: %s\n", err)
		return
	}
	fmt.Printf("Selected flavor: %s\n", flavor)
}
