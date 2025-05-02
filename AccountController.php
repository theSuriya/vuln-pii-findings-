<?php
namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;

class AccountController extends AbstractController
{
    public function showProfile($userId)
    {
        // In real app, fetch from database
        $profile = [
            'id' => $userId,
            'username' => 'john_doe',
            'ssn' => '987-65-4321',
            'email' => 'john.doe@domain.com'
        ];

        return new Response(json_encode($profile));
    }
}