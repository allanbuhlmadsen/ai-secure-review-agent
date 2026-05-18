using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.ComponentModel.DataAnnotations;

namespace FalsePositiveApi.Controllers
{
    public class FalsePositiveRequest
    {
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
    }

    [Authorize]
    [ApiController]
    [Route("api/false-positive")]
    public class FalsePositiveController : ControllerBase
    {
        private const string Token = "demo-value-used-for-testing-only";

        [HttpPost]
        public IActionResult Test(FalsePositiveRequest request)
        {
            return Ok();
        }
    }
}