using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;
using System.Data.SqlClient;

namespace SafeApi.Controllers
{
    public class UserRequest
    {
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
    }

    [Authorize]
    [ApiController]
    [Route("api/users")]
    public class SafeUserController : ControllerBase
    {
        private readonly string _connectionString;

        public SafeUserController(IConfiguration configuration)
        {
            _connectionString = configuration.GetConnectionString("DefaultConnection");
        }

        [HttpPost]
        public IActionResult GetUser(UserRequest request)
        {
            string query = "SELECT * FROM Users WHERE Username = @Username";

            SqlConnection connection = new SqlConnection(_connectionString);
            SqlCommand command = new SqlCommand(query, connection);
            command.Parameters.AddWithValue("@Username", request.Username);

            return Ok();
        }
    }
}