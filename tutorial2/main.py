#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, Token
from cdktf_cdktf_provider_aws.provider import AwsProvider

from cdktf_cdktf_provider_aws import vpc, subnet, instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        AwsProvider(self, 'aws', region='us-east-1')
        
        # Create VPC
        cdktf_vpc=vpc.Vpc(self, "cdktf_vpc", 
            cidr_block="10.0.0.0/16"
        )        
        
        # Create Public Subnet 
        cdktf_subnet = subnet.Subnet(self,"PublicSubnet01",
            vpc_id=Token.as_string(cdktf_vpc.id),
            cidr_block="10.0.0.0/24",
            map_public_ip_on_launch=True    #Make subnet public upon creation
            
        )
        
        # Create an EC2 instance with user_data
        # Code referenced from https://github.com/spacelift-io-blog-posts/Blog-Technical-Content/blob/master/cdktf-aws-python-webserver/main.py
        cdk_lab_web_instance= instance.Instance( self, "cdk_lab_web_instance",
            subnet_id=Token.as_string(cdktf_subnet.id),
            instance_type="t2.micro",
            ami="ami-0c101f26f147fa7fd",
            user_data="""#!/bin/bash
                sudo yum update -y
                sudo yum install httpd -y
                sudo systemctl enable httpd
                sudo systemctl start httpd
                echo "<html><body><div>Congrats you provisioned this web server with CDK for Terraform!</div></body></html>" > /var/www/html/index.html"""
        )

app = App()
MyStack(app, "tutorial2")

app.synth()
