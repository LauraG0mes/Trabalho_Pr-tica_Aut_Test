import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_generate_and_validate(driver):
    # Abrir a página HTML
    driver.get("http://127.0.0.1:5500/sample-exercise.html")

    # Clique no botão "generate"
    generate_button = driver.find_element(By.NAME, "generate")
    generate_button.click()

    # Aguarde até que o valor seja gerado em <p id="my-value">
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.find_element(By.ID, "my-value").text.strip() != "")

    # Obtenha o valor gerado
    my_value_element = driver.find_element(By.ID, "my-value")
    generated_value = my_value_element.text
    print(f"Valor gerado: {generated_value}")

    # Insira o valor gerado no campo <input id="input">
    input_field = driver.find_element(By.ID, "input")
    input_field.clear()
    input_field.send_keys(generated_value)

    # Clique no botão "test"
    test_button = driver.find_element(By.NAME, "button")
    test_button.click()

    # Lidar com o alerta
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    print(f"Texto do alerta: {alert.text}")
    alert.accept()  # Fecha o alerta clicando em "OK"

    # Aguarde a atualização do elemento <p id="result">
    wait.until(lambda d: "It workls!" in d.find_element(By.ID, "result").text)
    result_element = driver.find_element(By.ID, "result")
    assert "It workls!" in result_element.text, "Resultado esperado não encontrado"
