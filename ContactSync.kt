import java.io.File
import kotlinx.serialization.*
import kotlinx.serialization.json.*

@Serializable
data class Contact(val name: String, val email: String)

fun main() {
    val contacts = listOf(
        Contact("Peter Parker", "peter.parker@dailybugle.com"),
        Contact("Mary Jane", "mj.watson@dailybugle.com")
    )
    val json = Json.encodeToString(contacts)
    File("contacts.json").writeText(json)
}