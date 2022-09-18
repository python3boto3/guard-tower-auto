# guard-tower-auto

50 python security traps for GuardDuty threat message types

Traps for:

DefenseEvasion:IAMUser/AnomalousBehavior            ... DefenseEvasion:Kubernetes/MaliciousIPCaller

Persistence:Kubernetes/ContainerWithSensitiveMount  ... Persistence:Kubernetes/MaliciousIPCaller
Persistence:Kubernetes/MaliciousIPCaller.Custom     ... Persistence:Kubernetes/SuccessfulAnonymousAccess
Persistence:Kubernetes/TorIPCaller

Policy:IAMUser/RootCredentialUsage                  ... Policy:Kubernetes/AdminAccessToDefaultServiceAccount
Policy:Kubernetes/AnonymousAccessGranted            ... Policy:Kubernetes/ExposedDashboard
Policy:Kubernetes/KubeflowDashboardExposed          ... Policy:S3/AccountBlockPublicAccessDisabled
Policy:S3/BucketAnonymousAccessGranted              ... Policy:S3/BucketBlockPublicAccessDisabled

Trojan:EC2/DriveBySourceTraffic!DNS                 ... Trojan:EC2/DropPoint
Trojan:EC2/DropPoint!DNS                            ... Trojan:EC2/PhishingDomainRequest!DNS

UnauthorizedAccess:EC2/MaliciousIPCaller.Custom     ... UnauthorizedAccess:EC2/MetadataDNSRebind
UnauthorizedAccess:EC2/RDPBruteForce                ... UnauthorizedAccess:EC2/SSHBruteForce
UnauthorizedAccess:EC2/TorClient                    ... UnauthorizedAccess:EC2/TorRelay

UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B    ... UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS
UnauthorizedAccess:IAMUser/MaliciousIPCaller        ... UnauthorizedAccess:IAMUser/MaliciousIPCaller.Custom
UnauthorizedAccess:IAMUser/TorIPCaller              ... UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS

UnauthorizedAccess:S3/MaliciousIPCaller.Custom      ... UnauthorizedAccess:S3/TorIPCaller
