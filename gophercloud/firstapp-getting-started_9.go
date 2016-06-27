package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/rackspace/gophercloud"
	"github.com/rackspace/gophercloud/openstack"
	"github.com/rackspace/gophercloud/openstack/compute/v2/extensions/keypairs"
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

	const nameKeyPair string = "demokey"
	const filenamePubKey string = "/Users/bmorel/.ssh/bmorel@internap.com-key.pub"

	nova, err := openstack.NewComputeV2(provider, gophercloud.EndpointOpts{Region: config.Region})
	if err != nil {
		fmt.Println(err)
		return
	}

	var alreadyExists = false
	fmt.Printf("Checking if keypair named %s exists...\n", nameKeyPair)
	keypairs.List(nova).EachPage(func(page pagination.Page) (bool, error) {
		keypairList, err := keypairs.ExtractKeyPairs(page)
		if err != nil {
			return false, err
		}

		for _, currentKeypair := range keypairList {
			if strings.Contains(currentKeypair.Name, nameKeyPair) {
				alreadyExists = true
			}
		}
		return true, nil
	})
	if alreadyExists == true {
		fmt.Println("\t found keypair, skipping import")
		return
	}

	fmt.Println("\t importing keypair")
	keyContentByte, err := ioutil.ReadFile(filenamePubKey)
	if err != nil {
		panic(err)
	}
	strKeyContent := string(keyContentByte)
	kp, err := keypairs.Create(nova, keypairs.CreateOpts{Name: nameKeyPair, PublicKey: strKeyContent}).Extract()
	if err != nil {
		panic(err)
	}
	fmt.Printf("Keypair %s succesfully created\n", kp.Name)
}
