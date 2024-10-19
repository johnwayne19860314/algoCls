import java.util.Scanner;

public class RailFenceCipher {

    // Encrypt function for a single pass of the rail fence cipher
    public static String encryptRailFence(String message, int depth) {
        StringBuilder[] rail = new StringBuilder[depth];
        for (int i = 0; i < depth; i++) {
            rail[i] = new StringBuilder();
        }

        boolean down = false;
        int row = 0;

        for (char ch : message.toCharArray()) {
            rail[row].append(ch);

            if (row == 0 || row == depth - 1) {
                down = !down;
            }

            row = down ? row + 1 : row - 1;
        }

        StringBuilder encryptedMessage = new StringBuilder();
        for (StringBuilder sb : rail) {
            encryptedMessage.append(sb.toString());
        }

        return encryptedMessage.toString();
    }

    // Decrypt function for a single pass of the rail fence cipher
    public static String decryptRailFence(String encryptedMessage, int depth) {
        char[][] rail = new char[depth][encryptedMessage.length()];
        boolean down = false;
        int row = 0, col = 0;

        // Fill the rail matrix with '*' to mark positions
        for (int i = 0; i < encryptedMessage.length(); i++) {
            if (row == 0) {
                down = true;
            }
            if (row == depth - 1) {
                down = false;
            }

            rail[row][col++] = '*';

            row = down ? row + 1 : row - 1;
        }

        // Place encrypted characters into the marked positions
        int index = 0;
        for (int i = 0; i < depth; i++) {
            for (int j = 0; j < encryptedMessage.length(); j++) {
                if (rail[i][j] == '*' && index < encryptedMessage.length()) {
                    rail[i][j] = encryptedMessage.charAt(index++);
                }
            }
        }

        // Read the message in a zigzag manner
        StringBuilder result = new StringBuilder();
        row = 0;
        col = 0;
        for (int i = 0; i < encryptedMessage.length(); i++) {
            if (row == 0) {
                down = true;
            }
            if (row == depth - 1) {
                down = false;
            }

            if (rail[row][col] != 0) {
                result.append(rail[row][col++]);
            }

            row = down ? row + 1 : row - 1;
        }

        return result.toString();
    }

    // Repeated Rail Fence Encryption with multiple passes
    public static String repeatedRailFenceEncrypt(String message, int depth, int repeat) {
        message = message.toLowerCase();
        for (int i = 0; i < repeat; i++) {
            message = encryptRailFence(message, depth);
        }
        return message;
    }

    // Repeated Rail Fence Decryption with multiple passes
    public static String repeatedRailFenceDecrypt(String encryptedMessage, int depth, int repeat) {
        for (int i = 0; i < repeat; i++) {
            encryptedMessage = decryptRailFence(encryptedMessage, depth);
        }
        return encryptedMessage;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Input message
        System.out.print("Enter the message: ");
        String message = scanner.nextLine();

        // Input key (depth, repeats)
        System.out.print("Enter the key (depth, repeats): ");
        String[] keyInput = scanner.nextLine().split(",");
        int depth = Integer.parseInt(keyInput[0]);
        int repeat = Integer.parseInt(keyInput[1]);

        // Encrypt
        String encryptedMessage = repeatedRailFenceEncrypt(message, depth, repeat);
        System.out.println("Encrypted message: " + encryptedMessage);

        // Decrypt
        String decryptedMessage = repeatedRailFenceDecrypt(encryptedMessage, depth, repeat);
        System.out.println("Decrypted message: " + decryptedMessage);

        scanner.close();
    }
}
