using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class instantiate : MonoBehaviour
{
    public GameObject prefab;
    // Start is called before the first frame update
      Vector3 spawnPosition = new Vector3(2.0f, 0.0f, 3.0f);
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        for (var i = 0; i < 2; i++)
        {
           
            Instantiate(prefab, spawnPosition, Quaternion.identity);
        }
        
    }
}
