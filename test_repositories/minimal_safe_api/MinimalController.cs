using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MinimalSafeApi.Controllers
{
    [Authorize]
    [ApiController]
    [Route("api/minimal")]
    public class MinimalController : ControllerBase
    {
    }
}