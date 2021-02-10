## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |   Basic, 1 vCore(s), 50 GB        |  $5.31        |
| * webapp                  |   AppSvcPlanProject (F1: Free)    |       0       |
| * functionapp             |  EastUSLinuxDynamicPlan (Y1: 0)   |         0     |
| * Application Gateway     |     Standard                      |  $1.91        |
| *  storage                |        Standard/Hot               |  0.89         |
|    *event hubs            |         Basic                     |   0.85        |



Total cost per month estimate

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

Function
   Cost Effectiveness and Architectural decisions
      Functions are billed based on observed resource consumption measured in gigabyte seconds (GB-s). I selected the basic free tier for the Service Plan because in development, there is limited usage. While there is some cost, it is negligible. Cost for Execution Time of $0.000016/GB-s	4which allows 400,000 GB/second. This translates to $0.20 per million executions. Even in a prodution environment, the traffic is still limited. At most the cost would be < $20/ month for a function tied to the conference app, and most likely < 10. Using a VM was not an option as it was overkill both in cost as well as in function. My time translates to lost income if I have to spent time managing the OS and database systems. Additionally, the VM requires the use of more resources, which require management as well as cost.  The function itself especially with service bus is minimal code to maintain, easy changes and simply redeployment, so no resources required to house codebase.
Web
   Cost Effectiveness and Architecdtural decisions
      I selected the basic free tier the Service Plan to host my webapp because in development. The biggest drawback is that it is an "always pay for the service plan" so there is not really an on-off. However, there is limited usage. Even in a prodution environment, the traffic is still limited to hundreds.  I realize with a webapp I am unable to install specific software, have Limited access to the host server and underlying operating system. Using a VM was not an option as it was overkill both in cost as well as in function. My time translates to lost income if I have to spent time managing the OS and database systems. Additionally, the VM requires the use of more resources, which require management as well as cost.The hardware limitations of webapp easily satisfy the demands of the system. Compare VM vs webpp, for VM I used Number of VMs x Number of Hours Running = Cost. Whereas the webapp is F1 Free	Shared with (60 CPU minutes / day)	, 1 GB memory, and	1.00 GB storage with zero cost. If I ever needed to scale, I could move to the Shared tier, which is $0.013/hour.My selection for a Azure Post Gres Database costs $0.034/hour, but is only used during transactions, so compared to a VM is a streamline solution. Also data storage using Azure Post Gres is dirt cheap since it is only text. The webapp itself especially with service bus is minimal code to maintain if changes are needed, and simply updating. All resources are in the cloud and include autoamtic automatic updates and backups as there is no additional charge for backup storage for up to 100% of your total provisioned server storage. 





