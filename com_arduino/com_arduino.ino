
void setup() {
    Serial.begin(115200); //Initialisation de la communication avec le moniteur série
    Serial1.begin(115200);

    for (int pin = 22; pin <= 23; pin++) {
        pinMode(pin, INPUT_PULLUP);
    } 
}

void loop() { 
    String etatBtn = "";
    for (int pin = 22; pin <= 23; pin++) {
        int etat = digitalRead(pin);  // Lire l'état du pin
        etatBtn += String(etat);     // Ajouter l'état (0 ou 1) à la chaîne
    }
    Serial.println(etatBtn) ; // Affiche l’état du bouton sur le moniteur
    Serial1.println(etatBtn) ; // Affiche l’état du bouton sur le moniteur

    delay(1000) ; // Attente de 1000 ms
}
