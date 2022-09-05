from venmo_api import Client

# inputusername = input("What is your username: ")
# inputpassword = input("What is your password: ")

# Get your access token. You will need to complete the 2FA process
# access_token = Client.get_access_token(username=inputusername,
#                                        password=inputpassword)

def venmologin(venusername, venpassword):
    # Get your access token. You will need to complete the 2FA process
    access_token = Client.get_access_token(username=venusername, password=venpassword)

    venmo = Client(access_token=access_token)
    
    paymentmethods =[]
    p_methods = venmo.payment.get_payment_methods()
    for p_method in p_methods:
        paymentmethods.append(str(p_method))
        print(p_method)


    # test_str=str(store.readlines())
    test_str = (''.join(paymentmethods))

    # print(test_str)
    namesub = "name"
    namesearch = [i for i in range(len(test_str)) if test_str.startswith(namesub, i)] 
    namecard = []

    idsub = "id"
    idsearch = [i for i in range(len(test_str)) if test_str.startswith(idsub, i)] 
    idcard = []

    for namegapahead in namesearch:
        namegap = namegapahead
        while test_str[namegapahead] != ",":
            namegapahead+=1
        namecard.append(test_str[namegap+5:(namegapahead)])

    for idgapahead in idsearch:
        idgap = idgapahead
        while test_str[idgapahead] != ",":
            idgapahead+=1
        idcard.append(test_str[(idgap+3):(idgapahead)])
    

    out = dict()
    for i, name in enumerate(namecard):
        out[idcard[i]] = name
    

    # out["venmo"] = venmo    
    print(out)
    return out
    
    #print(namecard)
    #print(idcard)
    
    


def send_funds(vnum, vacct, vamount, vnote, venusername, venpassword):
    access_token = Client.get_access_token(username=venusername, password=venpassword)
    venmo = Client(access_token=access_token)    
    user = venmo.user.get_user_by_username(username=vacct)
    itsto = (user.id)
    try:
        venmo.payment.send_money(int(vamount), vnote, str(itsto), vnum)
        return "Payment Processed"
    
    except:
        return "Payment Failed"

