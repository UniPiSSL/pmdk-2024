using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class coinDelete : MonoBehaviour
{
    
    // Start is called before the first frame update
    void Start()
    {
      
    }

    // Update is called once per frame
    void Update()
    {
        

    }
    void OnTriggerEnter2D(Collider2D other) {
        
         if (other.CompareTag("player"))
        {
            Destroy(gameObject, 0f);
        }else if(other.CompareTag("car")){
             Destroy(gameObject, 0f);
             CoinSpawn.Instance.coinsSpawned = CoinSpawn.Instance.coinsSpawned - 1;
        }
        }
}
