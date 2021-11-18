from Chapter2 import Section00

if __name__ == "__main__":
    chapter = Section00()
    try :
        chapter.no_01()
        chapter.no_02()
    except Exception as e:
        print("Exception >>>>",e)