public class test5
{
    public static void main(String[] args) {
        char Hh = 'H';
        if (Hh == 'H'){
            boolean bool = true;
            bool = !bool;
            if (bool){
                System.out.println("x");
            }
            else if (!bool){
                float i = 0.1f;
                while (i < 1000.0f){
                    System.out.println(i);
                    i *= 2;
                    if (i > 500){
                        bool = !bool;
                    }
                }
                System.out.println(bool);
            }
        }
    }
}  