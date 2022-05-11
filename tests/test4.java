public class testfile
{
    public static void main(String[] args) {
        int[][][] threeDimensional = {{{1,2,3}, {4,5,6}}, {{7,8,9}, {10,11,12}}, {{13,14,15}, {16,17,18}}, {{19,20,21}, {22,23,24}}};
        System.out.println(threeDimensional[0][1][2]);
        for (int[][] twoDimensional : threeDimensional){
            System.out.println(twoDimensional);
            for (int[] oneDimensional : twoDimensional){
                System.out.println(oneDimensional);
            }
        }
        int x = 0;
        int y = (x+2)*(2);
        switch(x){
            case 0:
                System.out.println("0");
                switch(y){
                    case 4:
                        System.out.println("4");
                    default:
                        break;
                }
                break;
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
                break;
            case 3:
                System.out.println("3");
                break;
            case 4:
                System.out.println("4");
                break;
            default:
                break;
        }
    }
}  