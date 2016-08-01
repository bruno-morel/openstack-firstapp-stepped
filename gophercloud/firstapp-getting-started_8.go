package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
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

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println("Cleaning up servers for gophercloud...")
	servers.List(nova, servers.ListOpts{}).EachPage(func(page pagination.Page) (bool, error) {
		serverList, err := servers.ExtractServers(page)

		if err != nil {
			return false, err
		}

		for _, currentServer := range serverList {
			if strings.Contains(currentServer.Name, "gophercloud") {
				fmt.Printf("\t- deleting server with ID %s and name '%s'\n", currentServer.ID, currentServer.Name)
				servers.Delete(nova, currentServer.ID)
			}
		}
		return true, nil
	})
}
