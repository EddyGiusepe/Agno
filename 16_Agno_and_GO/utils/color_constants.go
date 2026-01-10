// Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

/*
Package utils fornece constantes e funções para colorir texto no terminal.
Este módulo define cores ANSI que podem ser usadas em outros scripts.

FORMATANDO O CÓDIGO
-------------------
gofmt -w colors.go

CONVENÇÕES DE NOMENCLATURA EM GO:
- PascalCase para símbolos exportados (públicos)
- camelCase para símbolos privados ao package

NOTA: Na linguagem GO, não é necessário declarar o 
      tipo de uma variável. O Go infere o tipo da variável
      automaticamente.

const (
		// Go vê "\033[0m" e sabe que é uma STRING automaticamente
		Reset  = "\033[0m"     // Tipo: string (inferido)
		Number = 42            // Tipo: int (inferido)
		Pi     = 3.14159       // Tipo: float64 (inferido)
		Active = true          // Tipo: bool (inferido)
	)
*/

package utils

// Constantes de cores ANSI exportadas (públicas)
// Seguindo a convenção PascalCase do Go
const (
	Reset  = "\033[0m"
	Red    = "\033[31m"
	Green  = "\033[32m"
	Yellow = "\033[33m"
	Blue   = "\033[34m"
	Purple = "\033[35m"
	Cyan   = "\033[36m"
	White  = "\033[37m"
)