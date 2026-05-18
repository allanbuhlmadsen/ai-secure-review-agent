using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;
using System.Data.SqlClient;

namespace SqlFalseNegativeApi.Controllers
{
    public class SqlFalseNegativeRequest
    {
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
    }

    [Authorize]
    [ApiController]
    [Route("api/sql-false-negative")]
    public class SqlFalseNegativeController : ControllerBase
    {
        [HttpPost]
        public IActionResult GetUser(SqlFalseNegativeRequest request)
        {
            string query = $"SELECT * FROM Users WHERE Username = '{request.Username}'";

            SqlConnection connection = new SqlConnection("Server=localhost;Database=Users;");
            SqlCommand command = new SqlCommand(query, connection);

            return Ok();
        }
    }
}