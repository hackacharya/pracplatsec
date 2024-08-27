
# Introduction

This document is created as a TODO/CHECKLIST for a security conscious product development team that is developing and deploying a product or service.

This document assumes a certain SaaS based service architecture, which is ubiquitous in this day and age. Several SaaS service deployments are done in the public clouds, such as GCP, AWS, Azure. A good percentage of saas services are deployed and operated out of private data centres / private clouds. While a lot of services continue to be deployed on virtual machine appliances there has been a major shift into deploying using a microservice kubernetes based architecture. This paper will consider that as the de facto deployment model . 

The responsibilities of addressing each item listed in this document may fall on different parties in the larger organisation. The platform or the operating system runtime system may address most of the table-stakes items, however this will vary based on the provider. And in case of Kubernetes being deployed by the product team itself this list becomes very useful. Even if the platform provider supports several of these, engineering teams and leaders should be aware and should know how a certain security topic is handled and supported by the platform. 

Note that this paper does not attempt to address application security.  No discussion is provided on each topic - a later version of the document may provide additional details, and possibly points on HOWTOs for each topic or checklist item.

In addition to security, this document maay contain a set of items that overlap with general saas/cloud deployment best practices.

This clearly is not an exhaustive list, but a very good starting point for buttressing your security. None of this is theory - all of this has been done/deployed used at some point by the author.

A JIRA import CSV version of this list, with priorities categories, and tags can be made available upon request.

