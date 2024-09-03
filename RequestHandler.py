# Matthew Buchanan
# Networking and Data Structures
# Spring 2019
# Project 1: udp client and server with threaded reliable connections to clients


# Function to handle user requests
def requestHandler(m, co, address):
    replyCode = "200  "
    mathReplyCode = "250  "
    syntaxError = "500  "
    parameterSyntaxError = "501  "
    badCommandSequence = "503  "

    if "CALC" == m[0:4] and len(m.split()) == 1:
        return replyCode + "CALC ready!", True
    elif "HELO" == m[0:4] and len(m.split()) == 1:
        return replyCode + "HELO  " + str(address[0]) + " (UDP)", co
    elif "HELP" == m[0:4] and len(m.split()) == 1:
        helpMessage = ("HELP\n" + "The 'HELO' command greets the server\n" +
        "The 'CALC' command turns on the Calculator functions\n" +
        "The 'POWER' command takes the form: POWER Base Exponent, ex. POWER 3 5\n" +
        "The 'CUBE' command takes the form: CUBE number and returns the cube root, ex. CUBE 9\n" +
        "The 'FACT' command takes the form: FACT number and returns number's factorial, ex. FACT 5\n" +
        "The 'BYE' command closes the client thread and exits the client")
        return helpMessage, co
    elif "CUBE" == m[0:4]:
        if len(m.split()) == 2:
            if co == False:
                return badCommandSequence + "CUBE before CALC", co
            a, b = m.split()
            answer = float(float(b) ** 1/3)
            answer = str(answer)
            return mathReplyCode + str(answer), co
        else:
            return parameterSyntaxError + "Parameter syntax error", co
    elif "FACT" == m[0:4]:
        if len(m.split()) == 2:
            if co == False:
                return badCommandSequence + "FACT before CALC", co
            a, b = m.split()
            b = int(b)
            answer = b
            for i in range(b - 1, 1, -1):
                answer *= i
            answer = str(answer)
            return mathReplyCode + str(answer), co
        else:
            return parameterSyntaxError + "Parameter syntax error", co
    elif "POWER" == m[0:5]:
        if len(m.split()) == 3:
            if co == False:
                return badCommandSequence + "POWER before CALC", co
            a, b, c = m.split()
            answer = pow(int(b), int(c))
            answer = str(answer)
            return mathReplyCode + str(answer), co
        else:
            return parameterSyntaxError + "Parameter syntax error", co
    elif "BYE" == m[0:3]:
        if len(m.split()) == 1:
            return replyCode + "BYE  " + str(address[0]) + " (UDP)", co
        else:
            return syntaxError + "Syntax error", co
    else:
        return syntaxError + "Syntax error", co