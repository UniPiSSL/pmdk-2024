using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;

public class finishSpawn : MonoBehaviour
{
    // Start is called before the first frame update
    
    [SerializeField] GameObject[] fruitPrefab;
    [SerializeField] float secondSpawn;// Added semicolon here

    [SerializeField] float minTrans;
    [SerializeField] float maxTrans;


    private bool boundarySpawn;
    private bool finishSpawned = true;
    void Start()
    {
        finishSpawned = true;
    }

    // Update is called once per frame
    void Update()
    {
       boundarySpawn = BoundariesSpawn.boundarySpawn;
       Debug.Log(boundarySpawn);
       if(!boundarySpawn){
            if (finishSpawned){
                StartCoroutine(FruitSpawn());
                finishSpawned = false;
            }
        }
    }
     IEnumerator FruitSpawn()
    {
            var wanted = Random.Range(minTrans, maxTrans);
            var position = new Vector3(wanted, transform.position.y);
            yield return new WaitForSeconds(secondSpawn);
            GameObject spawnedObject = Instantiate(fruitPrefab[Random.Range(0, fruitPrefab.Length)], position, Quaternion.identity);
            
            Destroy(spawnedObject, 5f);
    }
}