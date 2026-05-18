using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;
using System.Data.SqlClient;

namespace SecretOnlyApi.Controllers
{
    public class SecretRequest
    {
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
    }

    [Authorize]
    [ApiController]
    [Route("api/secrets")]
    public class SecretController : ControllerBase
    {
        private const string ApiKey = "my-secret-api-key-123";

        [HttpPost]
        public IActionResult GetSecret(SecretRequest request)
        {
            string query = "SELECT * FROM Users WHERE Username = @Username";

            SqlConnection connection = new SqlConnection("Server=localhost;Database=Users;");
            SqlCommand command = new SqlCommand(query, connection);
            command.Parameters.AddWithValue("@Username", request.Username);

            return Ok();
        }
    }
}