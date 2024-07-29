using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BoundariesSpawn : MonoBehaviour
{
    [SerializeField] GameObject[] fruitPrefab;
    [SerializeField] float secondSpawn = 0.5f;
    [SerializeField] float minTrans;
    [SerializeField] float maxTrans;
    
    private int coinsSpawnedValue;
    public static bool boundarySpawn = true;
    
    void Start()
    {
        boundarySpawn = true;
        coinsSpawnedValue = CoinSpawn.Instance.coinsSpawned;
        Debug.Log(coinsSpawnedValue);
        //StartCoroutine(FruitSpawn());
    }

    void Update(){
       coinsSpawnedValue = CoinSpawn.Instance.coinsSpawned;
       Debug.Log(coinsSpawnedValue);
       if(coinsSpawnedValue==3){
        if(boundarySpawn){
            StartCoroutine(FruitSpawn());
            WaitForSeconds a = new WaitForSeconds(2);
            boundarySpawn = false;
        }
        
       }
    }

    IEnumerator FruitSpawn()
    {                        

            var wanted = Random.Range(minTrans, maxTrans);
            var position = new Vector3(wanted, transform.position.y);
            GameObject spawnedObject = Instantiate(fruitPrefab[Random.Range(0, fruitPrefab.Length)], position, Quaternion.identity);
            yield return new WaitForSeconds(secondSpawn);
            
            Destroy(spawnedObject, 5f);
        
    }
}
