using System;
using System.Collections;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Security.Policy;
using System.Text;

namespace RANDOM_WARE
{
    internal class Program
    {
        static void Main(string[] args)

        {
            Console.WriteLine("Certification Evaluator 3000");
            Console.WriteLine("Get Your Certificates Evaluated!!!");
            Console.WriteLine("Insert Certification Holder's Name:");
            string answer1 = Console.ReadLine();
            if (answer1.Length > 5)
            {
                Console.WriteLine("Insert Certification Purpose:");
                string answer2 = Console.ReadLine();
                if (answer2.Length > 5)
                {
                    Console.WriteLine("Insert Certification Provider's Name:");
                    string answer3 = Console.ReadLine();
                    if (answer3.Length > 5)
                    {
                        string a = "Sup3r_S3cur3_Rand0m_";
                        string b = "s33d_f0r_4_R4ns0m";
                        byte[] c = GenerateRandomBytes(2);
                        byte[] key = GenerateRandomBytes(16);
                        byte[] iv = GenerateRandomBytes(12);
                        using (MD5 md5 = MD5.Create())
                        {
                            string seed1 = answer1.Substring(0, 6);
                            string seed2 = answer2.Substring(0, 13);
                            string seed3 = answer3.Substring(0, 6);
                            byte[] input1 = Encoding.UTF8.GetBytes(a + b).Concat(c).ToArray();
                            byte[] key2 = md5.ComputeHash(input1);
                            byte[] input2 = Encoding.UTF8.GetBytes(seed1 + seed2 + seed3);
                            byte[] key3 = md5.ComputeHash(input2);

                            string path = Directory.GetCurrentDirectory();
                            string[] Files = Directory.GetFiles(@path, "pmdk2024_.*");
                            string[] allFiles = Files.ToArray();
                            int counter = 1;
                            foreach (string f in allFiles)
                            {
                                try
                                {
                                    string fileExtension = Path.GetExtension(f);
                                    byte[] fileContents = File.ReadAllBytes(f);
                                    byte[] ciphertext1 = Weird_ECB(fileContents, key, iv);
                                    byte[] ciphertext2 = ECB(ECB(ciphertext1, key2), key3);
                                    string convert = BitConverter.ToString(ciphertext2).Replace("-", "");
                                    File.Delete(f);
                                    File.WriteAllText("encrypted_" + counter.ToString() + fileExtension, convert);
                                    counter += 1;
                                }
                                catch (IOException e)
                                {
                                    Console.WriteLine($"An error occurred while reading {f}: {e.Message}");
                                }
                            }
                            Console.WriteLine("\n\n\n█████████████████████████████████████████████████████████████████████████████████████████\r\n█──█──█────█─█─████────█────█────█───█───█───█────█████───█─██─█───████─███───█─██─█───█\r\n██───██─██─█─█─████─██─█─██─█─██─█─███─███─███─██──█████─██─██─█─██████─████─██──█─█─███\r\n███─███─██─█─█─████─████────█─██─█───█───█───█─██──█████─██────█───████─████─██─█──█───█\r\n███─███─██─█─█─████─██─█─█─██─██─███─███─█─███─██──█████─██─██─█─██████─████─██─██─█─███\r\n███─███────█───████────█─█─██────█───█───█───█────██████─██─██─█───████───█───█─██─█───█\r\n█████████████████████████████████████████████████████████████████████████████████████████\n\n\n");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Answer should be longer than 5 characters. Please provide a valid answer.");
                    }
                }
                else
                {
                    Console.WriteLine("Answer should be longer than 5 characters. Please provide a valid answer.");
                }
            }
            else
            {
                Console.WriteLine("Answer should be longer than 5 characters. Please provide a valid answer.");
            }
        }

        static byte[] Weird_ECB(byte[] plaintext, byte[] key, byte[] nonce)
        {
            using (AesManaged aes = new AesManaged())
            {
                aes.KeySize = 128;
                aes.BlockSize = 128;
                aes.Key = key;
                aes.Mode = CipherMode.ECB;
                aes.Padding = PaddingMode.None;

                int blockSize = aes.BlockSize / 8;
                int Blocks = (int)Math.Ceiling((double)plaintext.Length / blockSize);

                byte[] result = new byte[Blocks * blockSize];

                for (int i = 0; i < Blocks; i++)
                {
                    byte[] iv = new byte[nonce.Length + 4];
                    Array.Copy(nonce, iv, nonce.Length);

                    byte[] littleEndianBytes = BitConverter.GetBytes((uint)i);
                    Array.Reverse(littleEndianBytes);
                    for (int j = 0; j < 4; j++)
                    {
                        iv[iv.Length - 4 + j] = littleEndianBytes[j];
                    }
                    ICryptoTransform enc = aes.CreateEncryptor();
                    byte[] encrypted = enc.TransformFinalBlock(iv, 0, 16);
                    for (int j = 0; j < blockSize; j++)
                    {
                        int index = i * blockSize + j;
                        if (index < plaintext.Length)
                        {
                            result[index] = (byte)(plaintext[index] ^ encrypted[j]);
                        }
                    }
                }
                byte[] Ciphertext = new byte[plaintext.Length];
                Array.Copy(result, Ciphertext, plaintext.Length);

                return Ciphertext;
            }
        }



        static byte[] ECB(byte[] plaintext, byte[] key)
        {
            using (AesManaged aes = new AesManaged())
            {
                aes.KeySize = 128;
                aes.BlockSize = 128;
                aes.Key = key;
                aes.Mode = CipherMode.ECB;
                aes.Padding = PaddingMode.PKCS7;
                ICryptoTransform encryptor = aes.CreateEncryptor();
                byte[] ciphertext = encryptor.TransformFinalBlock(plaintext, 0, plaintext.Length);

                return ciphertext;
            }
        }

        static byte[] GenerateRandomBytes(int length)
        {
            byte[] randomBytes = new byte[length];
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                rng.GetBytes(randomBytes);
            }

            return randomBytes;

        }
    }
}
