package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/networks"
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

	const instanceName string = "testing for gophercloud"

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	var strNetLANLabel string
	fmt.Println("Looking for LAN network...")
	err = networks.List(nova).EachPage(func(page pagination.Page) (bool, error) {
		networkPage, err := networks.ExtractNetworks(page)
		if err != nil {
			return false, err
		}

		for _, currentNetwork := range networkPage {
			if strings.Contains(currentNetwork.Label, "WAN") {
				strNetLANLabel = currentNetwork.Label
			}
		}

		return true, nil
	})
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Printf("\t found network with name '%s'", strNetLANLabel)
	// step-13
	fmt.Println("Looking for instance...")
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

	if ptrServerFound == nil {
		fmt.Println("\tserver doesn't exists, failure")
		return
	}

	fmt.Printf("%v", ptrServerFound.Addresses[strNetLANLabel])
	fmt.Printf("%v", ptrServerFound.Addresses[strNetLANLabel].(servers.Network)["addr"])
	/*for i := range ptrServerFound.Addresses[strNetLANLabel] {
		fmt.Printf("(%s) %v\n", i, ptrServerFound.Addresses[strNetLANLabel][i])
	}*/
	fmt.Println("Done! Congrats")
}
