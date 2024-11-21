# **Auth**

Authentication is implement using Cognito service provided by the AWS.

## **Behaviours**:

- **Sign Up**: User will provide their credentials which will then go through a set of local validators, followed by the
request towards the Aws Cognito service. If any error occurs user will be notified about it with the appropriate message.
- **Sign In**: Access and Refresh token will be returned to the user, they will be stored in the cookie's storage.
- **Sign Out**: Call official Aws Cognito Api for sign-out, then proceed to remove the jwt tokens from the users cookies storage. 
- **Token Expired**: Sign out function provided by Boto3 client will be called to sign out the user from the Aws Cognito,
service followed by the removal of jwt tokens from the users cookie storage.

