from output_methods import MethodsOutput

def main():
    meo = MethodsOutput("./data/pessoas.mp4")
    #meo.camera()
    meo.width = 750
    meo.video()


if __name__ == '__main__':
    main()
