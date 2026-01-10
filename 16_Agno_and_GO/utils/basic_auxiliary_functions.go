// Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

/*
Package utils fornece funções utilitárias para operações com arrays e slices.
Este pacote é usado em outros scripts para realizar operações com arrays.

FORMATANDO O CÓDIGO
-------------------
gofmt -w basic_auxiliary_functions.go

NOTA:
Usamos CAMEL CASE em nossos nomes de funções e variáveis, já que estamos 
usando a linguagem Go.
*/

package utils

// EncontrarMaiorMenor encontra o maior e menor valor em um array de inteiros.
// Parâmetros:
//   - array: array de 7 inteiros
//
// Retorna o maior e menor valor encontrados.
func EncontrarMaiorMenor(numericalValues [7]int) (int, int) { // Usando "camelCase" --> numericalValues
	maior := numericalValues[0]
	menor := numericalValues[0]

	for _, valor := range numericalValues {
		if valor > maior {
			maior = valor
		}
		if valor < menor {
			menor = valor
		}
	}
	return maior, menor
}

// CalculaMedia calcula a média aritmética de um array de float64.
// Parâmetros:
//   - array: array de 5 float64
//
// Retorna a média dos valores.
func CalculaMedia(numbers [5]float64) float64 { // Sem usar camelCase --> numbers
	soma := 0.0
	for _, valor := range numbers {
		soma = soma + valor
	}
	return soma / float64(len(numbers))
}

// SomarElementos retorna a soma de todos os elementos de um array de inteiros.
// Parâmetros:
//   - array: array de inteiros
//
// Retorna a soma dos valores.
func SomarElementos(values []int) int {
	soma := 0
	for _, valor := range values {
		soma += valor
	}
	return soma
}

// ContarElementos conta quantas vezes um elemento aparece no array de inteiros.
// Parâmetros:
//   - array: array de inteiros
//   - elemento: elemento a ser contado
//
// Retorna o número de vezes que o elemento aparece no array.
func ContarElementos(values []int, elemento int) int {
	contador := 0
	for _, valor := range values {
		if valor == elemento {
			contador++
		}
	}
	return contador
}
