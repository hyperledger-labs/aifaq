# -*- coding: utf-8 -*-

from utils import load_yaml_file

# Read config data
config_data = load_yaml_file("config.yaml")

def gethomepage():
    markdown_string = f"""
<div style="text-align: center;">
  <img src={config_data["logo_pth"]} alt="AIFAQ logo" style="height: 110px">
  <h1>AI Agent powered by <em>Founder Institute</em></h1>
</div>

## Try for free

Here the [Official GitHub Repository](https://github.com/hyperledger-labs/aifaq)

## Links and Resources

AIFAQ Inc. [website](https://aifaqpro.wordpress.com/)

## Founder Institute

This chatbot is a Founder Institute conversational AI tool. Please, register or login:
"""
    return markdown_string
