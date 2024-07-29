using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CoinSpawn : MonoBehaviour
{
    [SerializeField] GameObject[] fruitPrefab;
    [SerializeField] float secondSpawn = 0.5f;

    public int coinsSpawned = 0;
    [SerializeField] float minTrans;
    [SerializeField] float maxTrans;
    [SerializeField] float minSecSpawn;
    [SerializeField] float maxSecSpawn;

    public static CoinSpawn Instance;

    void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

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
            GameObject spawnedObject = Instantiate(fruitPrefab[Random.Range(0, fruitPrefab.Length)], position, Quaternion.identity);
            yield return new WaitForSeconds(secondSpawn);
            coinsSpawned++;
            secondSpawn = Random.Range(minSecSpawn, maxSecSpawn);
            Destroy(spawnedObject, 5f);
        }
    }
}
