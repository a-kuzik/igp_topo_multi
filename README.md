# igp_topo_multi

IGP topology with NeXt UI
 This is not the first network topology drawing tool that use the NeXt UI.
 The NeXt UI Toolkit is an HTML5 / JavaScript based toolbox for networked web applications.
 https://creations.devnetcloud.com/detail?cid=1e4a9f92-deea-11e7-9d2f-aed03b171102
 https://github.com/NeXt-UI
 
This small project contains Python script and templates for parsing IGP LSDB (OSPF and ISIS) such vendors as Nokia, Juniper, Cisco and Huawei, creating topology in json format for drawing network topology in NeXt UI and showing it in your browser.

Using this script is very easy.

1) Please load a file with LSDB in directory ```/test_files```. Currently contains the few tests files.
2) In the file config.yaml specify the path and name to your LSDB file, vendor name, where did you get the LSDB file, and type of IGP (OPSF or ISIS).
3) Runnig the script  ```igp_topo_light.py``` and enjoy your network topology in a browser.

Currently supported:

- Nokia - OSPF and ISIS;
- Juniper - OSPF and ISIS;
- Cisco - OSPF and ISIS;
- Huawei - ISIS.

Following commands outputs are possible for parsing:

Nokia:

```show router isis database detail```

```show router ospf database type router detail```

Juniper:

```show isis database extensive```

```show ospf database router detail```

Cisco:

```show isis database detail```

```show ip ospf database router```

Huawei:

```display isis lsdb verbose```
