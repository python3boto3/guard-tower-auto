import json
import boto3


def lambda_handler(event, context):

    # Consumed message from origin sns ... generated through GD setup
    # *************************************************************************
    message = event['Records'][0]['Sns']['Message']
    sns = boto3.client('sns', region_name='us-east-2')
    arn = "arn:aws:sns:us-east-2:704231384733:guard-duty-sns-notification"

    # find strType
    # *************************************************************************
    # first get a 100 characterdeep mid from the original string
    mLen = len(message)-100
    # 100 to the length of the string-100
    findtypeStr2 = message[100:mLen]
    # locate the keyword 'remoteIpDetails'
    findtypeInt = findtypeStr2.find('type')
    # locate the keyword 'resourcetype'
    findresourceInt = findtypeStr2.find('resourceType')-findtypeInt
    # trim the output
    strType = findtypeStr2[findtypeInt+7:findtypeInt+findresourceInt-15]

    # findipStr
    # *************************************************************************
    # first get a 100 characterdeep mid from the original string
    mLen = len(message)-100
    # 100 to the length of the string-100
    findtypeStr2 = message[100:mLen]
    # locate the keyword 'type'
    findtypeInt = findtypeStr2.find('remoteIpDetails')
    # locate the keyword 'organization'
    findresourceInt = findtypeStr2.find('organization')-findtypeInt
    # trim the output
    ipType = findtypeStr2[findtypeInt+33:findtypeInt+findresourceInt-3]

    # findportStr
    # *************************************************************************
    # first get a 100 characterdeep mid from the original string
    mLen = len(message)-100
    # 100 to the length of the string-100
    findtypeStr2 = message[100:mLen]
    # locate the keyword 'localPortDetails'
    findtypeInt = findtypeStr2.find('localPortDetails')
    # locate the keyword 'resourcetype'
    findresourceInt = findtypeStr2.find('portName')-findtypeInt
    # trim the output
    portType = findtypeStr2[findtypeInt+26:findtypeInt+findresourceInt-2]
    # type from the message
    typeStr2 = strType
    # ip address from message
    ipStr2 = ipType
    # extract port number from nmessage
    portStr2 = portType

    # Add the 3 variable values found above, to the code to delete
    # *************************************************************************

    # ec2_c.create_network_acl_entry(CidrBlock='222.188.19.221/32',
    # Egress=False,NetworkAclId='acl-0b4a0451675bc9e31',
    # PortRange={'From': 80, 'To': 80,},Protocol='6',
    # RuleAction='allow',RuleNumber=99)

    ec2 = boto3.resource('ec2')
    ec2_c = boto3.client('ec2', region_name='us-east-2')
    sb3 = boto3.resource('s3', region_name='us-west-2')
    bucket = sb3.Bucket('lambda-static-data')
    # get decrement value in bucket key
    for obj in bucket.objects.all():
        key = obj.key
        if key == "guard-duty-000.txt":
            decInt = obj.get()['Body'].read()

    # decrement the nacl entry number – it is on rotate
    decInt2 = int(decInt)-1

    'recycle nacl entries'
    if int(decInt2) < 94:
        decInt3 = 99
    else:
        decInt3 = int(decInt2)

    # pass the decInt2 value into the update nacl entry command
    ec2_c.replace_network_acl_entry(
        CidrBlock=ipType + '/32',
        Egress=False,
        NetworkAclId='acl-0b4a0451675bc9e31',
        PortRange={'From': int(portType), 'To': int(portType), }, Protocol='6',
        RuleAction='deny',
        RuleNumber=decInt3
        )

    #  the static data key with the new working value.
    decStr = str(decInt3)
    content = decStr
    sb3.Object('lambda-static-data', "guard-duty-000.txt").put(Body=content)

    # Add the 3 variable values found above,
    # to the code to inform users via sns, send the sns publish
    # *************************************************************************

    errMsg1 = 'IP Address was blocked using NACL acl-0b4a0451675bc9e31 on \
        uPunch-Production (UPunch C).' + '\r' + '\r' + 'Attack Type: ' \
        + typeStr2 + '\r' + 'Blocked Remote IP address: ' + ipStr2 + '\r' \
        + 'Port: ' + portStr2 + '\r' + '\r' + 'Original message from \
        GuardDuty, below:' + '\r' + '\r' + message

    errMsg2 = 'A remote attacker was blocked.'
    response = sns.publish(
        TargetArn=arn,
        Message=json.dumps(
            {
                'default': json.dumps(message),
                'sms': errMsg1,
                'email': errMsg1
            }
        ),
        Subject=errMsg2,
        MessageStructure='json'
        )

    # Blocks the Bad IPs WACL on the ohio waf classic regional ip-set
    # *************************************************************************

    client2 = boto3.client('waf-regional', region_name='us-east-2')

    ipSetId = '0e5a4acd-01b0-44be-9e5a-e6b70c5deae4'

    response = client2.get_change_token()
    rr = response['ChangeToken']

    print(rr)

    response = client2.get_ip_set(IPSetId=ipSetId)
    update_sets = []
    ipType2 = ipType + '/32'
    i = {'Type': 'IPV4', 'Value': ipType2}
    v = {
            'Action': 'INSERT',
            'IPSetDescriptor': i
        }
    update_sets.append(v)

    print(update_sets)

    if len(update_sets) > 0:
        client2.update_ip_set(
            IPSetId=ipSetId,
            ChangeToken=rr,
            Updates=update_sets
        )
