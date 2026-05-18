using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace DuplicateSecretApi.Controllers
{
    public class DuplicateSecretRequest
    {
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
    }

    [Authorize]
    [ApiController]
    [Route("api/duplicate-secrets")]
    public class DuplicateSecretController : ControllerBase
    {
        private const string ApiKey = "duplicate-secret-api-key-123";
        private const string BackupApiKey = "duplicate-backup-api-key-456";

        [HttpPost]
        public IActionResult GetSecret(DuplicateSecretRequest request)
        {
            return Ok();
        }
    }
}