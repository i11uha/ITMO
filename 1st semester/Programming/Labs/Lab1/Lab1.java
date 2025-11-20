import java.util.Arrays;
import java.util.Random;

class LaboratoryWork1 {

    // Метод для вычисления очередного элемента двумерного массива
    public static double calculateElement(int sValue, double xValue) {
        if (sValue == 22) {
            return Math.log((2 + Math.pow(Math.cos(xValue), 2)) / 2 * Math.PI);
        }
        else if (sValue == 6 || sValue == 8 || sValue == 12 || sValue == 16 || sValue == 18) {
            return Math.exp(Math.exp(Math.log(Math.abs(xValue))));
        }
        else {
            double q = (xValue - 2.5) / 25.0;
            return Math.log(Math.pow(2 * Math.acos(q * q), Math.atan(Math.cos(xValue))));
        }
    }

    // Метод для вывода матрицы
    public static void printMatrix(double[][] matrix) {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(" ");
                System.out.printf("%8.3f", matrix[i][j]);
            }
            System.out.println();
        }
    }

    public static void main(String[] args) {
        // Exercise 1
        int size = ((24-6)/2)+1;
        int[] s = new int[size];
        for (int i = 0; i < s.length; i++) {
            s[i] = 6 + i * 2;
        }
        System.out.print("Exercise 1:");
        System.out.println(Arrays.toString(s));
        System.out.print("\n");

        // Exercise 2
        float[] x = new float[19];
        Random random = new Random();

        for (int j = 0; j < x.length; j++) {
            x[j] = random.nextFloat() * 25.0f - 15.0f; // (10.0 - (-15.0)) = 25.0
        }
        System.out.print("Exercise 2:");
        System.out.println(Arrays.toString(x));
        System.out.print("\n");

        // Exercise 3 and 4
        double[][] s1 = new double[10][19];

        for (int a = 0; a < s1.length; a++) {
            for (int b = 0; b < s1[a].length; b++) {
                int sv = s[a]; // sv => S-Value
                double xv = x[b]; // xv => X-Value

                // Используем отдельный метод для вычисления элемента
                s1[a][b] = calculateElement(sv, xv);
            }
        }

        System.out.println("Exercise 3 and 4:");
        // Используем отдельный метод для вывода матрицы
        printMatrix(s1);
    }
}