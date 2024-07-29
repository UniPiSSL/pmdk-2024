using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class flagScreen : MonoBehaviour
{
    public GameObject flag;
    public TextMeshProUGUI nope;
    int score;
    // Start is called before the first frame update
    void Start()
    {
        score = gameHandler.score;
    }

    // Update is called once per frame
    void Update()
    {
        if (score >= 10000) {
            flag.SetActive(true);
        }
        else {
            nope.enabled = true;
        }
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Application.Quit();
        }
    }
}
