# mongo-migration

This repository is used for Mongo Migration Automation.

Fill up the ".vars.yml" file with appropriate entries as explained below:

Sample ".vars.yml"

---
```
---
variables:

  ansibletags:    "validate" # Ansible tags.Fill one of setup, validate, cutover, datavalidate, rollback
  
```     

### Variables are explained below:
Mandatory variables are marked '*' before the variable name.

***ansibletags**       - Mandatory. Fill this with one of setup, validate, cutover, rollback


### How to run mongo-migration pipeline?


#### Setup Destination Nodes as Secondary Mongo cluster Nodes

    ansibletags: "setup"
    
    Setup the Destination nodes as Secondary Nodes to the cluster with priority as zero.

#### Validate

    ansibletags: "validate"

    Shows the status of the Mongo Cluster with Nodes health, state ( Primary/Secondary/Recovering etc), uptime and if any lastheartbeatMessage.

#### Cutover

    ansibletags: "cutover"

    Step Down the master and promote one of the destination nodes as Primary Node to the Cluster.

#### DataValidation

    ansibletags: "datavalidate"

    Mongo Cluster Data Validation using MD5 Hash Comparison.

#### Rollback

    ansibletags: "rollback"

    Step down the existing Primary Node and promote one of the source nodes as the Primary node for the Mongo Cluster.

