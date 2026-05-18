using Microsoft.AspNetCore.Mvc;
using System.Data.SqlClient;

namespace VulnerableApi.Controllers
{
    [ApiController]
    [Route("api/users")]
    public class UserController : ControllerBase
    {
        private const string ConnectionString =
            "Server=localhost;Database=Users;User Id=admin;Password=SuperSecretPassword123;";

        [HttpGet]
        public IActionResult GetUser(string username)
        {
            string query =
                "SELECT * FROM Users WHERE Username = '" + username + "'";

            SqlConnection connection = new SqlConnection(ConnectionString);

            SqlCommand command = new SqlCommand(query, connection);

            return Ok();
        }
    }
}