<?php
namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class UserUpdater
{
    public function modify(Request $request): Response
    {
        $data = json_decode($request->getContent(), true);

        $payload = [
            'id' => $data['id'],
            'full_name' => $data['full_name'],
            'email' => $data['email'],
            'dob' => $data['dob'],
            'ssn' => $data['ssn'],
            'creditCard' => $data['creditCard']
        ];

        return new Response(json_encode(['status' => 'success', 'data' => $payload]), 200, ['Content-Type' => 'application/json']);
    }
}