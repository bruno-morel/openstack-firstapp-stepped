package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/networks"
	"github.com/rackspace/gophercloud/openstack/compute/v2/flavors"
	"github.com/rackspace/gophercloud/openstack/compute/v2/images"
	"github.com/rackspace/gophercloud/openstack/compute/v2/servers"
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

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	flavor, err := flavors.Get(nova, "A1.1").Extract()

	image, err := images.Get(nova, "3c76334f-9644-4666-ac3c-fa090f175655").Extract()

	var netwan networks.Network
	count := 0
	err = networks.List(nova).EachPage(func(page pagination.Page) (bool, error) {
		currentNetwork, err := networks.ExtractNetworks(page)
		if err != nil {
			return false, err
		}
		if strings.Contains(currentNetwork[count].Label, "WAN") {
			netwan = currentNetwork[count]
		}
		count++
		return true, nil
	})

	server, err := servers.Create(nova, servers.CreateOpts{Name: "second test instance for gophercloud", FlavorRef: flavor.ID, ImageRef: image.ID, Networks: []servers.Network{servers.Network{UUID: netwan.ID}}}).Extract()
	if err != nil {
		fmt.Printf("Unable to create server: %s", err)
	}
	fmt.Printf("Created server with ID: %s", server.ID)

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
}
