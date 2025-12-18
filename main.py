def main(tokens:list):
    stack = []

    for token in tokens: # listni for da aylantiramiz   
        if token in {"+", "-", "*", "/"}: #  token shu belgilar borligini tekshiramiz
            b = stack.pop() # stackdan oxirgi elementni olib tashlaymiz
            a = stack.pop() # stackdan ikkinchi oxirgi elementni olib tashlaymiz

            if token == "+": #  token teksiramiz +  == ligini 
                stack.append(a + b) # agar ten bolsa stack + a + b
            elif token == "-": #  
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:  # '/'
                stack.append(int(a / b)) 
        else:
            stack.append(int(token))

    return stack[0]
