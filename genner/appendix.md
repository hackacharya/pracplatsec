# Appendix A - Kubernetes server options to review.  
  
Kubernetes server and the kubelet commands provide a lot of options to fine tune security related configuration. This configuration needs to be reviewed in every kubernetes environment. A set of security related options are provided here for review - always refer to the latest kubernetes documentation   
  
Reference: https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/  
  
As of March 2024.  
  
    --anonymous-auth  
    --audit-policy-file  
    --authentication-config  
    --authorization-config  
    --authorization-mode  
    --authorization-policy-file  
    --authorization-webhook-config-file  
    --bind-address  
    --client-ca-file  
    --cors-allowed-origins  
    --enable-admission-plugins  
    --encryption-provider-config  
    --etcd-cafile  
    --etcd-certfile  
    --kubelet-certificate-authority  
    --kubelet-client-certificate  
    --oidc-ca-file  
    --oidc-signing-algs  
    --peer-ca-file  
    --root-ca-file  
    --service-account-extend-token-expiration  
    --service-account-key-file  
    --service-account-max-token-expiration  
    --strict-transport-security-directives  
    --tls-cipher-suites  
    --tls-private-key-file  
    --tls-sni-cert-key  
    --use-service-account-credentials  
