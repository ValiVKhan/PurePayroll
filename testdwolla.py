import dwollafull
import dwollav2
from time import sleep
client = dwollav2.Client(
  key = '',
  secret = '',
  environment = 'sandbox', # defaults to 'production'
)
application_token = client.Auth.client()

#Testing creating a verified customer
# v, w = dwollafull.createemployer('Business2','Owner','BizzOwner@email.com','143.156.7.8','business','1980-01-31','6789','99-99 33rd St','Some City', 'NY', '11101', '9ed3f670-7d6f-11e3-b1ce-5404a6144203', 'soleProprietorship', 'Amal', '11-1111111','222222226','987654321','checking', 'ThisIsMyBank')
# v,w = dwollafull.createemployer('Business2','Owner','BizzOwner2@email.com','143.156.7.8','business','1980-01-31','6789','99-99 33rd St','Some City', 'NY', '11101', '9ed3f670-7d6f-11e3-b1ce-5404a6144203', 'soleProprietorship', 'MyBusiness', '11-1111111','222222226','987654321','checking', 'BusinessBankAcctName')
# print(v,w)

#Testing creating an employee and getting their funding source
# z,y = dwollafull.createemplyee('Vali','tmith','ParseRetun8@gmail.com','222222226','987654321','checking', 'ZeeAcctName')
# dwollaid = z.split("/",4)
# dwollasid = y.split("/",4)
# print ("The customer's dwolla id is: " + dwollaid[4])
# print ("The customer's dwolla source id is: " + dwollasid[4])
# sleep(3)
# v = dwollafull.verifyemployer(v,w,0.03,0.09)

# print(v)


#     funding_sources = application_token.get('%s/funding-sources' % employercustomerid)
    # return (funding_sources.body['_embedded']['funding-sources'][0]['status'])



# Using dwollav2 - https://github.com/Dwolla/dwolla-v2-python
# funding_source_url = w
# h = application_token.get(funding_source_url)

# print(h.body)
# application_token.post('%s/micro-deposits' % funding_source_url)

# request_body = {
#     'amount1': {
#         'value': '0.03',
#         'currency': 'USD'
#     },
#     'amount2': {
#         'value': '0.09',
#         'currency': 'USD'
#     }
# }

# application_token.post('%s/micro-deposits' % funding_source_url, request_body)

# h = application_token.get(funding_source_url)

# print(h.body)

# #Testing making a transaction
# q = dwollafull.transfer('https://api-sandbox.dwolla.com/funding-sources/36b8b539-451a-4def-971a-99b162d90741', 
# funding_source_url, '10','first tansfer through functions')
# print(q)
# print("sleeping...")
# sleep(45)
t = dwollafull.transfer('https://api-sandbox.dwolla.com/funding-sources/643000b2-d689-4f31-ab3b-d8258cc2721d', 'https://api-sandbox.dwolla.com/funding-sources/7375a852-faa2-431c-92dd-bf06864eb7dd', '10.55','note','note')
# print(t)

# dummylist =[('url1','1','12345678','hello'),('url1','1','12345678','hello'),('url1','1','12345678','hello'),('url1','1','12345678','hello'),('url1','1','12345678','hello')]


# dwollafull.masstransfer('url of source', dummylist)
