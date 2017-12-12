from colorama import Fore
import build_json_coords


def main():
    # TODO: Setup mongoengine global values

    print_header()

    try:
        while True:
            if find_user_intent() == 'split':
                build_json_coords.run_split()
            else:
                build_json_coords.run_elevations()
    except KeyboardInterrupt:
        return


def print_header():
    python = \
        """
             ~8I?? OM               
            M..I?Z 7O?M             
            ?   ?8   ?I8            
           MOM???I?ZO??IZ           
          M:??O??????MII            
          OIIII$NI7??I$             
               IIID?IIZ             
  +$       ,IM ,~7??I7$             
I?        MM   ?:::?7$              
??              7,::?778+=~+??8       
??Z             ?,:,:I7$I??????+~~+    
??D          N==7,::,I77??????????=~$  
~???        I~~I?,::,77$Z?????????????  
???+~M   $+~+???? :::II7$II777II??????N 
OI??????????I$$M=,:+7??I$7I??????????? 
 N$$$ZDI      =++:$???????????II78  
               =~~:~~7II777$$Z      
                     ~ZMM~ """

    print(Fore.WHITE + '****************  SNAKE BnB  ****************')
    print(Fore.GREEN + python)
    print(Fore.WHITE + '*********************************************')
    print()
    print("Welcome to the File Creation Portal!")
    print("Why are you here?")
    print()


def find_user_intent():
    print("[s] Split geojson file into line segments")
    print("[e] Add elevations to file")
    print()
    choice = input()
    if choice == 's':
        return 'split'

    return 'elevations'


if __name__ == '__main__':
    main()