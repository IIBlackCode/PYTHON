class Section00:
    
    def no_01(self):
        print("\n\n[1] 변수와 print() 함수")
        print("안녕하세요?")
        print("1. 100")
        print("2. %d" % 100)
        print("3. 100 + 100")
        print("4. %d" % (100+100))      # TypeError: can only concatenate str (not "int") to str
        # print("5. %d" % (100,200))    # TypeError: not all arguments converted during string formatting
        # print("6. %d %d" % (100))     # TypeError: not enough arguments for format string
        print("7. %d %d" % (100, 200))
        
        print("\n\n input()함수는 모든 것을 문자열로 간주해서 입력받는다.")
        print("var1 :")
        var1 = input()
        print("var2 :")
        var2 = input()
        print("RESULT :",var1 + var2)
        
        print("\n\n input()함수로 숫자를 입력받는 방법")
        print("var1 :")
        var1 = int(input())
        print("var2 :")
        var2 = int(input())
        print("RESULT :",var1 + var2)
        
        print("\n\n input(\"설명\")")
        var1 = int(input("숫자를 입력 해 주세요 :"))
        var2 = int(input("숫자를 입력 해 주세요 :"))
        print("RESULT :",var1 + var2)
        
        

        
    def no_02(self):
        print("\n\n[2] 연산자")
        
        a = 5 ; b = 3
        print(a+b, a-b, a*b, a/b, a//b, a%b, a**b)
        # print("a=5, b=3\n a+b=%d, a-b=%d, a*b=%d, a/b=%f, a//b=%d, a'%'b=%d, a**b=%d" % ((a+b), (a-b), (a*b), (a/b), (a//b), (a%b), (a**b)))
        #(8, 2, 15, 1.6666666666666667, 1, 2, 125)
        
    def no_03(self):
        print("\n\n[2] 연산자")
    def no_04(self):
        print("\n\n[2] 연산자")
    def no_05(self):
        print("\n\n[2] 연산자")
    def no_06(self):
        print("\n\n[2] 연산자")
    

    