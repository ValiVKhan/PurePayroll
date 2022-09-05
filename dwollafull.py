
from time import sleep
from pprint import pprint as pp
import dwollav2
# Create dwolla client object
client = dwollav2.Client(
  key = 'A8PrXAX1kFM0hHktY3l8FYWPX8KZQMiB7zBgiyXeC09AO082EM',
  secret = 'E1cyNdJsjKm0IIv7MIwwAQchpTqtP7dP3YoTPY6bKichigm7EG',
  environment = 'sandbox', # defaults to 'production'
)

# Application Token
application_token = client.Auth.client()

#All data comes as strings even numbers!!!

#Creating an employer as DWOLLA customer, this is a verified customer in DWOLLA
def createemployer(erfirstname, erlastname, eremail, erip, ertype, erdob, erssn, eraddress1, ercity, erstate, erpostalcode, erbusinessclassify, erbusinesstype, erbusinessname, erein, eroutingnum, eaccountnum, eaccounttype, eaccountname):
    request_body = {
        'firstName': erfirstname,
        'lastName': erlastname,
        'email': eremail,
        'ipAddress': erip,
        'type': ertype,
        'dateOfBirth': erdob,
        'ssn': erssn,
        'address1': eraddress1,
        'city': ercity,
        'state': erstate,
        'postalCode': erpostalcode,
        'businessClassification': erbusinessclassify,
        'businessType': erbusinesstype,
        'businessName': erbusinessname,
        'ein': erein
    }

    vcustomer = application_token.post('customers', request_body)

    vcustomer_id = vcustomer.headers['Location']

    #Create customer bank account
    request_body = {
        'routingNumber': eroutingnum,
        'accountNumber': eaccountnum,
        'bankAccountType': eaccounttype,
        'name': eaccountname
        }
    customer = application_token.post('%s/funding-sources' % vcustomer_id, request_body)
    
    vcustomerfund_id = customer.headers['Location']
    
    #Initiate transfer
    application_token.post('%s/micro-deposits' % vcustomerfund_id)
    sleep(3)
    return vcustomer_id,vcustomerfund_id


#Verify the micro deposit
def verifyemployer(employercustomerid, employercustomerfundid, enteredamount1, enteredamount2):
    request_body = {
    'amount1': {
        'value': enteredamount1,
        'currency': 'USD'
    },
    'amount2': {
        'value': enteredamount2,
        'currency': 'USD'
    }
    }

    application_token.post('%s/micro-deposits' % employercustomerfundid, request_body)

    funding_sources = application_token.get('%s/funding-sources' % employercustomerid)
    verification_status = (funding_sources.body['_embedded']['funding-sources'][0]['status'])
    return(verification_status)

    


#Create employee as DWOLLA customer and add their bank account
def createemplyee(efirstname, elastname, eemail, eroutingnum, eaccountnum, eaccounttype, eaccountname):
    #Create customer
    application_token = client.Auth.client()
    customerdata = application_token.post('customers', { 
        'firstName': efirstname, 
        'lastName': elastname, 
        'email': eemail, 
         'type': "receive-only" 
        })

    customer_id = customerdata.headers['Location']

    #Create customer bank account

    request_body = {
        'routingNumber': eroutingnum,
        'accountNumber': eaccountnum,
        'bankAccountType': eaccounttype,
        'name': eaccountname
        }
    customer = application_token.post('%s/funding-sources' % customer_id, request_body)
    
    customerfund_id = customer.headers['Location']
    
    return customer_id,customerfund_id


#Transfer from employer to employee
def transfer(transourceid, trandestinationid, value, paymentid, note):
    request_body = {
        '_links': 
        {
            'source': {
            'href': transourceid
            },
            'destination': {
            'href': trandestinationid
            }
        },
        'amount': 
        {
            'currency': 'USD',
            'value': value
        },
        'metadata': 
        {
            'paymentId': paymentid,
            'note': note
        },
        'achDetails': {
            # 'source': {
            # 'addenda': {
            #     'values': ['withdrawal for' + paymentid]
            # }
            # },
            # 'destination': {
            # 'addenda': {
            #     'values': [paymentid+" "+ note]
            # },
            # },
        },
        'clearing': 
        {
            'source': 'next-available',
            'destination': 'next-available'
        }
    }

    transfer = application_token.post('transfers', request_body)
    
    transaction_id=transfer.headers['Location']
    return transaction_id


emptylist = []

def masstransfer(employerfundingsourceurl, destinationslist):
    for line in destinationslist:
        d={
        '_links': {
            'destination': {
            'href': line[0]
            }
        },
        'amount': {
            'currency': 'USD',
            'value': line[1]
        },
        'clearing': {
            'destination': 'next-available'
        },
        'correlationId': 'ad6ca82d-59f7-45f0-a8d2-94c2cd4e8841',
        'achDetails': {
            'addenda': {
            'values': [line[2]+" "+ line[3]]
            }
        },
        }
        emptylist.append(d)
    request_body = {
    '_links': {
    'source': 
    {
        'href': employerfundingsourceurl
    }
    },
    'achDetails': {
    'addenda': {
        'values': ['ABC123_AddendaValue']
    }
    },
    'clearing': {
    'source': 'standard'
    },
    'items': emptylist,
    } 
    pp(request_body)   


