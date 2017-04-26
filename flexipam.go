package main

import {
	"encoding/xml"
	"fmt"
}

type Operations struct {
	operator string
}


type Protocol struct {
	
	Name string `xml:"name"`
	Addresses []struct {
		Street string `xml:"street"`
		City   string `xml:"city"`
		Type   string `xml:"type,attr"`
	} `xml:"addresses>address"`
}



func main() {

	fmt.Println("FLEXIPAM")

	baseDir = "sample-config/"
	protocolDir = baseDir + "protocols/"
	protocolName = "login.protocol"
	protocolPath = protocolDir + "login.protocol"
	
	protocolFile, err := os.Open(protocolPath)
	if err != nil {
		fmt.Println("Error opening file", protocolPath, ":", err)
		return
	}
	defer protocolFile.Close()
	
	var protocol Protocol
	xml.Unmarshal(protocolFile, &protocol)

}
