using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class carSpawn : MonoBehaviour
{
    [SerializeField] GameObject[] fruitPrefab;
    [SerializeField] float secondSpawn = 0.5f; // Added semicolon here

    [SerializeField] float minTrans;
    [SerializeField] float maxTrans;
    [SerializeField] float minSecSpawn;
    [SerializeField] float maxSecSpawn;
    
    void Start()
    {
        StartCoroutine(FruitSpawn());
    }

    IEnumerator FruitSpawn()
    {
        while (true)
        {
            var wanted = Random.Range(minTrans, maxTrans);
            var position = new Vector3(wanted, transform.position.y);
            GameObject spawnedObject = Instantiate(fruitPrefab[Random.Range(0, fruitPrefab.Length)], position, Quaternion.identity); // Corrected "length" to "Length"
            yield return new WaitForSeconds(secondSpawn);
            secondSpawn = Random.Range(minSecSpawn, maxSecSpawn);
            Destroy(spawnedObject, 5f);
        }
    }
}
