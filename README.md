# Mettler Toledo Scale
This program connects to a Mettler Toledo Scale and displays the weight in tons. If there is more than one scale configured it displays the total combined weight. This type of scale is used on multi-stage weigh bridges.

Run once to generate a config file. The program can support one or more scales, example of a remote scale configuration:

> [scale1]  
> host = localhost 
> port = 1749  
>
> [scale2]  
> host = 10.0.0.101  
> port = 1749  

![image](https://user-images.githubusercontent.com/30706122/213860647-2cba4694-46a9-4a7d-b115-9fb74c396fcf.png)

Included in the repo is a PowerShell build script that generates a .exe and .msi

## server.py
Approximate stand in for Scale Server ran locally. Set config ip to 127.0.0.1.
Used for debugging.
