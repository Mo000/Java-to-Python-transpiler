public class test3
{
    public static void main(String[] args) 
    {
        testFunc();
    }
    public static void testFunc(){
        int e = ("hello").length();
        for (int i=0; i<10000; i = i+1){
            System.out.println(i);
            System.out.println(e);
        }
    }
} 