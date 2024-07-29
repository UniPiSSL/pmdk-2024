using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

public class gameHandler : MonoBehaviour
{
    public static int score = 0;
    public TextMeshProUGUI ValueText;
    

    void Start()
    {
      
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Application.Quit();
        }
        
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("coin"))
        {
            score = score + 1;
            ValueText = GameObject.Find("/Canvas/Score").GetComponent<TextMeshProUGUI>();
            ValueText.text = score.ToString();
        }
        else if (other.CompareTag("car"))
        {
            score = 0;
            Scene currentScene = SceneManager.GetActiveScene();
            SceneManager.LoadScene(currentScene.buildIndex);
        }
        else if (other.CompareTag("finish"))
        {
            SceneManager.LoadScene("flag");
        }
        
    }
    void Reset()
    {
        Scene currentScene = SceneManager.GetActiveScene();
        SceneManager.LoadScene(currentScene.buildIndex);
    }

    void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.CompareTag("car"))
        {
        score = 0; // Reset the score to 0

        // Reload the current scene
        Invoke("Reset", 0);
        
        }
        
    }
    
}
